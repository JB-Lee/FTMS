package org.cnsl.ftms.viewmodel

import android.content.Context
import androidx.lifecycle.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.cnsl.ftms.net.RequestHelper
import org.cnsl.ftms.repository.local.entities.Client
import org.cnsl.ftms.repository.remote.entities.FileItem
import org.cnsl.ftms.utils.LiveArrayList
import java.text.DecimalFormat
import java.text.SimpleDateFormat
import java.util.*
import kotlin.collections.ArrayList
import kotlin.math.floor
import kotlin.math.ln
import kotlin.math.pow

class TransferViewModel(val context: Context, val client_a: Client, val client_b: Client) : ViewModel(),
    LifecycleObserver {
    val aFiles = LiveArrayList<FileItem>()
    val bFiles = LiveArrayList<FileItem>()

    val aPath = MutableLiveData<String>()
    val bPath = MutableLiveData<String>()

    var session: String = ""

    @OnLifecycleEvent(Lifecycle.Event.ON_CREATE)
    fun onInit() {
        viewModelScope.launch(Dispatchers.IO) {

            RequestHelper("host", 8088).apply {
                var result = asyncRequest(
                    method = "getUuid",
                    session = null,
                    params = null,
                ).get("result") as Map<*, *>
                session = result["uuid"] as String

                val asAPath = async {
                    val res = asyncRequest(
                        method = "get_root",
                        session = "abc",
                        params = mapOf(
                            "header" to mapOf(
                                "from" to client_a.id,
                                "requester" to "abc"
                            )
                        ),
                    ).get("result") as Map<*, *>
                    println(res["cwd"] as String)
                    return@async res["cwd"] as String
                }

                val asBPath = async {
                    val res = asyncRequest(
                        method = "get_root",
                        session = "ab2",
                        params = mapOf(
                            "header" to mapOf(
                                "from" to client_b.id,
                                "requester" to "ab2"
                            )
                        ),
                    ).get("result") as Map<*, *>
                    println(res["cwd"] as String)
                    return@async res["cwd"] as String
                }

                withContext(Dispatchers.Main) {
                    aPath.value = asAPath.await()
                    bPath.value = asBPath.await()
                }

                val asAFile = async {
                    val res = asyncRequest(
                        method = "get_dir",
                        session = "a",
                        params = mapOf(
                            "header" to mapOf(
                                "from" to client_a.id,
                                "requester" to "a"
                            ),
                            "path" to aPath.value
                        ),
                    ).get("result") as Map<*, *>

                    val list = ArrayList<FileItem>()

                    (res["dirs"] as List<*>).forEach {
                        it as Map<*, *>
                        list.add(
                            FileItem(
                                it["name"] as String, it["size"] as Int, it["is_file"] as Boolean,
                                it["last_modified"] as Int
                            )
                        )
                    }

                    return@async list
                }

                val asBFile = async {
                    val res = asyncRequest(
                        method = "get_dir",
                        session = "b",
                        params = mapOf(
                            "header" to mapOf(
                                "from" to client_b.id,
                                "requester" to "b"
                            ),
                            "path" to bPath.value
                        ),
                    ).get("result") as Map<*, *>

                    val list = ArrayList<FileItem>()

                    (res["dirs"] as List<*>).forEach {
                        it as Map<*, *>
                        list.add(
                            FileItem(
                                it["name"] as String, it["size"] as Int, it["is_file"] as Boolean,
                                it["last_modified"] as Int
                            )
                        )
                    }

                    return@async list
                }

                withContext(Dispatchers.Main) {
                    aFiles.value = asAFile.await()
                    bFiles.value = asBFile.await()
                }


            }

            withContext(Dispatchers.Main) {

            }
        }

    }

    fun getFormattedSize(size: Int): String {
        val s = arrayOf("bytes", "KB", "MB", "GB", "TB", "PB")
        var retFormat = "0"

        if (size != 0) {
            val idx = floor(ln(size.toDouble()) / ln(1024.0))
            val df = DecimalFormat("#,###.##")
            val ret = ((size / 1024.0.pow(floor(idx))))
            retFormat = df.format(ret) + " " + s[idx.toInt()]
        } else {
            retFormat += " " + s[0]
        }

        return retFormat
    }

    fun convertToTime(time: Int): String {
        val date = Date(time.toLong() * 1000)
        val format = SimpleDateFormat("yyyy.MM.dd HH:mm", Locale.KOREA)
        return format.format(date)
    }
}