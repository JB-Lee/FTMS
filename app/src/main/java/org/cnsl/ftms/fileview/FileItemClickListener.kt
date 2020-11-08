package org.cnsl.ftms.fileview

import androidx.recyclerview.widget.RecyclerView

interface FileItemClickListener {
    fun onClick(item: FileItem, holder: RecyclerView.ViewHolder)
}