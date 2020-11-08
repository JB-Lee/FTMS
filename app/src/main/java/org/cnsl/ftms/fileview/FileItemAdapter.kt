package org.cnsl.ftms.fileview

import android.content.Context
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.RecyclerView
import kotlinx.android.synthetic.main.fileitem_view.view.*
import org.cnsl.ftms.R

class FileItemAdapter(
    private val context: Context,
    private val fileItems: ArrayList<FileItem>,
    private val listener: FileItemClickListener
) : RecyclerView.Adapter<FileItemAdapter.ViewHolder>(), ItemActionListener {

    private lateinit var target: FileItemAdapter

    class ViewHolder(val fileView: View) : RecyclerView.ViewHolder(fileView)

    fun setTarget(target: FileItemAdapter) {
        this.target = target
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val fileView = LayoutInflater.from(parent.context)
            .inflate(R.layout.fileitem_view, parent, false) as View
        return ViewHolder(fileView)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.fileView.tv_filename.text = fileItems[position].name
        holder.fileView.img_filetype.setImageDrawable(
            context.getDrawable(
                if (fileItems[position].isFile) R.drawable.ic_baseline_file_24 else R.drawable.ic_baseline_folder_24
            )
        )
        holder.fileView.setOnClickListener {
            Log.i("chek", "onBindViewHolder: $position")
            if (position < fileItems.size)
                listener.onClick(fileItems[position], holder)
        }

    }

    override fun getItemCount(): Int = fileItems.size

    override fun onItemMoved(
        recyclerView: RecyclerView,
        viewHolder: RecyclerView.ViewHolder,
        target: RecyclerView.ViewHolder
    ) {
        val from: Int = viewHolder.adapterPosition
        val to: Int = target.adapterPosition

        val fromItem = fileItems.removeAt(from)
        fileItems.add(to, fromItem)
        notifyItemMoved(from, to)
    }

    override fun onItemSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {
        val position: Int = viewHolder.adapterPosition

        if (direction == ItemTouchHelper.START) {
            target.fileItems.add(fileItems.removeAt(position))
            notifyDataSetChanged()
            target.fileItems.sortWith(compareBy(FileItem::isFile, FileItem::name))
            target.notifyDataSetChanged()
        } else
            notifyItemChanged(position)
    }

    fun changeItems(newItems: Collection<FileItem>) {
        fileItems.clear()
        fileItems.addAll(newItems)
        fileItems.sortWith(compareBy(FileItem::isFile, FileItem::name))
        notifyDataSetChanged()
    }


}