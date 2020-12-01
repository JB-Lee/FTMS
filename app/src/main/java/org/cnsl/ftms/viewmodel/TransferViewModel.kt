package org.cnsl.ftms.viewmodel

import android.content.Context
import androidx.lifecycle.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.cnsl.ftms.repository.local.entities.Client
import org.cnsl.ftms.repository.remote.database.FileItemDatabase
import org.cnsl.ftms.repository.remote.entities.FileItem
import org.cnsl.ftms.utils.LiveArrayList
import java.text.DecimalFormat
import java.text.SimpleDateFormat
import java.util.*
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

            FileItemDatabase.getInstance(context).getFileItemDao().apply {
                session = getUUID()

                val aPathFut = async { getRootPath(client_a.id, session) }
                val bPathFut = async { getRootPath(client_b.id, session) }

                val aPathTmp = aPathFut.await()
                val bPathTmp = bPathFut.await()

                val aFileFut = async { getFileList(client_a.id, aPathTmp, session) }
                val bFileFut = async { getFileList(client_b.id, bPathTmp, session) }

                withContext(Dispatchers.Main) {
                    aPath.value = aPathTmp
                    bPath.value = bPathTmp
                    aFiles.value = aFileFut.await() as ArrayList<FileItem>
                    bFiles.value = bFileFut.await() as ArrayList<FileItem>
                }

//                val aPathTmp = getRootPath(client_a.id, session)
//                val bPathTmp = getRootPath(client_b.id, session)
//                val aFilesTmp = getFileList(client_a.id, aPathTmp, session) as ArrayList<FileItem>
//                val bFilesTmp = getFileList(client_b.id, bPathTmp, session) as ArrayList<FileItem>
//
//                withContext(Dispatchers.Main) {
//                    aPath.value = aPathTmp
//                    bPath.value = bPathTmp
//                    aFiles.value = aFilesTmp
//                    bFiles.value = bFilesTmp
//                }
//

            }
        }
    }

    fun onItemClick(index: Int, item: FileItem) {
        if (item.isFile)
            return

        viewModelScope.launch(Dispatchers.IO) {
            FileItemDatabase.getInstance(context).getFileItemDao().apply {
                if (index == 0) {
                    val tmpPath = aPath.value + "\\" + item.name
                    val fileFut = async { getFileList(client_a.id, tmpPath, session) }

                    withContext(Dispatchers.Main) {
                        aPath.value = tmpPath
                        aFiles.value = fileFut.await() as ArrayList<FileItem>
                    }
                } else if (index == 1) {
                    val tmpPath = bPath.value + "\\" + item.name
                    val fileFut = async { getFileList(client_b.id, tmpPath, session) }

                    withContext(Dispatchers.Main) {
                        bPath.value = tmpPath
                        bFiles.value = fileFut.await() as ArrayList<FileItem>
                    }
                }

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