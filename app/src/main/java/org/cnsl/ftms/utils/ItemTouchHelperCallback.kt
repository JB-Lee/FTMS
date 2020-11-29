package org.cnsl.ftms.utils

import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.RecyclerView

class ItemTouchHelperCallback : ItemTouchHelper.Callback() {

    private val listeners: ArrayList<ItemActionListener> = ArrayList()

    fun addListener(listener: ItemActionListener): ItemTouchHelperCallback {
        listeners.add(listener)
        return this
    }

    override fun getMovementFlags(recyclerView: RecyclerView, viewHolder: RecyclerView.ViewHolder): Int {
        val dragFlags = ItemTouchHelper.DOWN or ItemTouchHelper.UP
        val swipeFlags = ItemTouchHelper.START or ItemTouchHelper.END
        return makeMovementFlags(dragFlags, swipeFlags)
    }

    override fun onMove(
        recyclerView: RecyclerView,
        viewHolder: RecyclerView.ViewHolder,
        target: RecyclerView.ViewHolder
    ): Boolean {
        listeners.forEach { it.onItemMoved(recyclerView, viewHolder, target) }
        return true
    }

    override fun onSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {
        listeners.forEach { it.onItemSwiped(viewHolder, direction) }
    }


}