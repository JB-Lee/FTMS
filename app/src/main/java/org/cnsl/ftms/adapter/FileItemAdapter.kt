package org.cnsl.ftms.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.lifecycle.ViewModel
import androidx.recyclerview.widget.RecyclerView
import org.cnsl.ftms.databinding.ItemFileListBinding
import org.cnsl.ftms.repository.remote.entities.FileItem
import org.cnsl.ftms.viewmodel.TransferViewModel

class FileItemAdapter(val vm: ViewModel, val index: Int) : RecyclerView.Adapter<FileItemViewHolder>() {
    private val items = ArrayList<FileItem>()

    override fun onBindViewHolder(holder: FileItemViewHolder, position: Int) {
        holder.bind(items[position])
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): FileItemViewHolder {
        val fileItemListBinding = ItemFileListBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return FileItemViewHolder(fileItemListBinding, vm, index)
    }

    override fun getItemCount(): Int = items.size

    fun clear() {
        items.clear()
    }

    fun add(data: FileItem) {
        items.add(data)
        items.sortWith(compareBy(FileItem::isFile, FileItem::name))
    }

    fun addAll(vararg data: FileItem) {
        items.addAll(data)
        items.sortWith(compareBy(FileItem::isFile, FileItem::name))
    }

    fun get(index: Int): FileItem = items[index]
}


class FileItemViewHolder(
    private val fileItemListBinding: ItemFileListBinding,
    private val vm: ViewModel,
    private val index: Int
) :
    RecyclerView.ViewHolder(fileItemListBinding.root) {

    fun bind(fileItem: FileItem) {
        fileItemListBinding.file = fileItem
        fileItemListBinding.vm = vm as TransferViewModel
        fileItemListBinding.index = index
        fileItemListBinding.executePendingBindings()
    }
}