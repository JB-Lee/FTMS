package org.cnsl.ftms.databinding

import androidx.databinding.BindingAdapter
import androidx.recyclerview.widget.RecyclerView
import org.cnsl.ftms.adapter.FileItemAdapter
import org.cnsl.ftms.repository.remote.entities.FileItem

object FileDataBinding {

    @JvmStatic
    @BindingAdapter("files")
    fun bindFileLists(view: RecyclerView, items: List<FileItem>?) {
        view.adapter.run {
            if (this is FileItemAdapter) {
                val adapterModel: FileItemAdapter = this

                adapterModel.clear()
                if (items != null) {
                    adapterModel.addAll(*items.toTypedArray())
                }

                this.notifyDataSetChanged()
            }
        }
    }

}