package org.cnsl.ftms.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.lifecycle.ViewModel
import androidx.recyclerview.widget.RecyclerView
import org.cnsl.ftms.databinding.ItemClientListBinding
import org.cnsl.ftms.repository.local.entities.Client
import org.cnsl.ftms.viewmodel.ManageViewModel

class ClientListAdapter(val vm: ViewModel, val buttonAvailable: Boolean) : RecyclerView.Adapter<ClientViewHolder>() {
    private val items = ArrayList<Client>()

    override fun onBindViewHolder(holder: ClientViewHolder, position: Int) {
        holder.bind(items[position])
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ClientViewHolder {
        val itemClientListBinding = ItemClientListBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ClientViewHolder(itemClientListBinding, vm, buttonAvailable)
    }

    override fun getItemCount(): Int = items.size

    fun clear() {
        items.clear()
    }

    fun add(data: Client) {
        items.add(data)
    }

    fun addAll(vararg data: Client) {
        items.addAll(data)
    }

    fun get(index: Int): Client = items[index]
}


class ClientViewHolder(
    private val itemClientListBinding: ItemClientListBinding,
    private val vm: ViewModel,
    private val buttonAvailable: Boolean
) :
    RecyclerView.ViewHolder(itemClientListBinding.root) {

    fun bind(client: Client) {
        itemClientListBinding.client = client
        itemClientListBinding.vm = vm as ManageViewModel
        itemClientListBinding.executePendingBindings()
        itemClientListBinding.btnItemEdit.visibility = if (buttonAvailable) View.VISIBLE else View.INVISIBLE
        itemClientListBinding.btnItemEdit.isClickable = buttonAvailable
    }
}