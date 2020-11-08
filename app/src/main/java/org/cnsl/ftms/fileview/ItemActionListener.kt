package org.cnsl.ftms.fileview

import androidx.recyclerview.widget.RecyclerView

interface ItemActionListener {
    fun onItemMoved(
        recyclerView: RecyclerView,
        viewHolder: RecyclerView.ViewHolder,
        target: RecyclerView.ViewHolder
    )

    fun onItemSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int)
}