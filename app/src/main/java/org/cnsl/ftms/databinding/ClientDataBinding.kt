package org.cnsl.ftms.databinding

import androidx.databinding.BindingAdapter
import androidx.recyclerview.widget.RecyclerView
import org.cnsl.ftms.adapter.ClientListAdapter
import org.cnsl.ftms.repository.local.entities.Client

object ClientDataBinding {

    @JvmStatic
    @BindingAdapter("client_items")
    fun bindClientLists(view: RecyclerView, items: List<Client>?) {
        view.adapter.run {
            if (this is ClientListAdapter) {
                val adapterModel: ClientListAdapter = this

                adapterModel.clear()
                if (items != null) {
                    adapterModel.addAll(*items.toTypedArray())
                }

                this.notifyDataSetChanged()
            }
        }
    }
}