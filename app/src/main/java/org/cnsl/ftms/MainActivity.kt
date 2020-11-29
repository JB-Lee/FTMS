package org.cnsl.ftms

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import org.cnsl.ftms.fileview.FileItemAdapters
import org.cnsl.ftms.fileview.FileItemClickListener
import org.cnsl.ftms.net.RequestHelper
import org.cnsl.ftms.repository.remote.entities.FileItem
import org.cnsl.ftms.utils.ItemActionListener
import org.cnsl.ftms.utils.ItemTouchHelperCallback

class MainActivity : AppCompatActivity(), FileItemClickListener {

    private lateinit var viewAdapter_1: FileItemAdapters
    private lateinit var viewAdapter_2: FileItemAdapters
    private lateinit var viewManager_1: RecyclerView.LayoutManager
    private lateinit var viewManager_2: RecyclerView.LayoutManager

    private lateinit var itemTouchHelper_1: ItemTouchHelper
    private lateinit var itemTouchHelper_2: ItemTouchHelper

    private val items_1: ArrayList<FileItem> = ArrayList()
    private val items_2: ArrayList<FileItem> = ArrayList()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

//        items_1.add(FileItem(false, "AAA", 100, 10000))
//        items_1.add(FileItem(true, "abc.zip", 100, 10000))
//        items_1.add(FileItem(true, "abd.zip", 100, 10000))
//
//        items_2.add(FileItem(false, "BBB", 100, 10000))
//        items_2.add(FileItem(true, "abe.zip", 100, 10000))
//        items_2.add(FileItem(true, "abc.zip", 100, 10000))

        viewManager_1 = LinearLayoutManager(this)
        viewManager_2 = LinearLayoutManager(this)
        viewAdapter_1 = FileItemAdapters(this, items_1, this)
        viewAdapter_2 = FileItemAdapters(this, items_2, this)

        viewAdapter_1.setTarget(viewAdapter_2)
        viewAdapter_2.setTarget(viewAdapter_1)

        itemTouchHelper_1 = ItemTouchHelper(
            ItemTouchHelperCallback()
                .addListener(viewAdapter_1 as ItemActionListener)
        )
        itemTouchHelper_1.attachToRecyclerView(recycler_view_1)

        itemTouchHelper_2 = ItemTouchHelper(
            ItemTouchHelperCallback()
                .addListener(viewAdapter_2 as ItemActionListener)
        )
        itemTouchHelper_2.attachToRecyclerView(recycler_view_2)

        recycler_view_1.apply {
            setHasFixedSize(false)
            layoutManager = viewManager_1
            adapter = viewAdapter_1
        }
        recycler_view_2.apply {
            setHasFixedSize(false)
            layoutManager = viewManager_2
            adapter = viewAdapter_2
        }

        CoroutineScope(Dispatchers.IO).apply {

        }



        btn_main.setOnClickListener {
            Thread {
                var id = ""
                RequestHelper("host", 8088)
                    .request(
                        method = "getUuid",
                        session = null,
                        params = null,
                        onSuccess = {
                            runOnUiThread { Toast.makeText(this, it.toString(), Toast.LENGTH_SHORT).show() }
                            val result = it.get("result") as Map<*, *>
                            id = result["uuid"] as String
                        },
                        onFail = null
                    )
                    .request(
                        method = "listdir",
                        session = id,
                        params = mapOf(
                            "header" to mapOf(
                                "from" to "client-a",
                                "to" to "client-a",
                                "requester" to id
                            ),
                            "path" to "C://Temp"
                        ),
                        onSuccess = {
                            runOnUiThread {
                                Toast.makeText(this, it.toString(), Toast.LENGTH_SHORT).show()

                                val result = it.get("result") as Map<*, *>
                                val filelist = result["dirs"] as List<*>

                                val items = ArrayList<FileItem>()
//                                for (filename in filelist)
//                                    items.add(
//                                        FileItem(true, filename as String, 100, 100)
//                                    )
                                viewAdapter_1.changeItems(items)

                            }
                        },
                        onFail = null
                    )

            }.start()

//            val items = ArrayList<FileItem>()
//            items.add(
//                FileItem(false, "abc", 100, 100)
//            )
//            viewAdapter_1.changeItems(items)
        }


    }

    override fun onClick(item: FileItem, holder: RecyclerView.ViewHolder) {
        Toast.makeText(this, item.name, Toast.LENGTH_SHORT).show()
    }
}