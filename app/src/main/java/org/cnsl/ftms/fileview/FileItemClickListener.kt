package org.cnsl.ftms.fileview

import androidx.recyclerview.widget.RecyclerView
import org.cnsl.ftms.repository.remote.entities.FileItem

interface FileItemClickListener {
    fun onClick(item: FileItem, holder: RecyclerView.ViewHolder)
}