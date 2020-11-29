package org.cnsl.ftms.view

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.ItemTouchHelper
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import kotlinx.android.synthetic.main.activity_manage.*
import org.cnsl.ftms.R
import org.cnsl.ftms.adapter.ClientListAdapter
import org.cnsl.ftms.databinding.ActivityManageBinding
import org.cnsl.ftms.repository.local.entities.Client
import org.cnsl.ftms.utils.ItemActionListener
import org.cnsl.ftms.utils.ItemTouchHelperCallback
import org.cnsl.ftms.viewmodel.ManageViewModel
import org.koin.android.ext.android.inject
import java.util.*

class ManageActivity : AppCompatActivity() {

    val viewModel: ManageViewModel by inject()
    val binding: ActivityManageBinding by lazy { DataBindingUtil.setContentView(this, R.layout.activity_manage) }
    var isFabOpen = false

    lateinit var animMainFabClose: Animation
    lateinit var animMainFabOpen: Animation
    lateinit var animSubFabClose: Animation
    lateinit var animSubFabOpen: Animation

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        animMainFabClose = AnimationUtils.loadAnimation(this, R.anim.fab_main_close)
        animMainFabOpen = AnimationUtils.loadAnimation(this, R.anim.fab_main_open)
        animSubFabClose = AnimationUtils.loadAnimation(this, R.anim.fab_sub_close)
        animSubFabOpen = AnimationUtils.loadAnimation(this, R.anim.fab_sub_open)

        binding.apply {
            vm = viewModel
            lifecycleOwner = this@ManageActivity
        }

        rv_client_list.apply {
            adapter = ClientListAdapter(viewModel, true)
            layoutManager = LinearLayoutManager(super.getBaseContext())
            addItemDecoration(DividerItemDecoration(this@ManageActivity, LinearLayoutManager.VERTICAL))
        }

        rv_selected_list.apply {
            adapter = ClientListAdapter(viewModel, false)
            layoutManager = LinearLayoutManager(super.getBaseContext())
            addItemDecoration(DividerItemDecoration(this@ManageActivity, LinearLayoutManager.VERTICAL))
        }


        ItemTouchHelper(
            ItemTouchHelperCallback().addListener(object : ItemActionListener {
                override fun onItemMoved(
                    recyclerView: RecyclerView,
                    viewHolder: RecyclerView.ViewHolder,
                    target: RecyclerView.ViewHolder
                ) {
                    TODO("Not yet implemented")
                }

                override fun onItemSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {
                    if (viewModel.selectClients.size < 2) {
                        val position = viewHolder.adapterPosition
                        viewModel.selectClients.add(
                            (rv_client_list.adapter as ClientListAdapter).get(position)
                        )
                        rv_selected_list.adapter!!.notifyItemInserted(position)
                    }

                    checkSelect()

                    rv_client_list.adapter!!.notifyDataSetChanged()
                }

            })
        ).attachToRecyclerView(rv_client_list)

        ItemTouchHelper(
            ItemTouchHelperCallback().addListener(object : ItemActionListener {
                override fun onItemMoved(
                    recyclerView: RecyclerView,
                    viewHolder: RecyclerView.ViewHolder,
                    target: RecyclerView.ViewHolder
                ) {
                    TODO("Not yet implemented")
                }

                override fun onItemSwiped(viewHolder: RecyclerView.ViewHolder, direction: Int) {
                    val position = viewHolder.adapterPosition
                    viewModel.selectClients.removeAt(position)

                    checkSelect()

                    rv_selected_list.adapter!!.notifyItemRemoved(position)
                }

            })
        ).attachToRecyclerView(rv_selected_list)

        srl_client_list.setOnRefreshListener {
            viewModel.onClientRefresh(srl_client_list)
            rv_client_list.adapter!!.notifyDataSetChanged()
            rv_selected_list.adapter!!.notifyDataSetChanged()
        }


        lifecycle.addObserver(viewModel)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == 1 && resultCode == Activity.RESULT_OK) {
            val client = data!!.getParcelableExtra<Client>("client")

            if (client != null) {
                viewModel.clients.add(client)
            }
        } else if (requestCode == 2) {
            if (resultCode == Activity.RESULT_OK) {
                val client = data!!.getParcelableExtra<Client>("client")

                if (client != null) {
                    viewModel.clients.add(client)
                }
            } else {
                if (viewModel.onEdit != null) {
                    viewModel.clients.add(viewModel.onEdit!!)
                    viewModel.onEdit = null
                }
            }

        }
    }

    fun toggleFab() {
        if (isFabOpen) {
            fab_manage_main.startAnimation(animMainFabClose)
            fab_manage_add_client.startAnimation(animSubFabClose)
            fab_manage_transfer.startAnimation(animSubFabClose)
            fab_manage_add_client.isClickable = false
            fab_manage_transfer.isClickable = false
            isFabOpen = false
        } else {
            fab_manage_main.startAnimation(animMainFabOpen)
            fab_manage_add_client.startAnimation(animSubFabOpen)
            fab_manage_transfer.startAnimation(animSubFabOpen)
            fab_manage_add_client.isClickable = true
            fab_manage_transfer.isClickable = true
            isFabOpen = true
        }
    }

    fun checkSelect() {
        binding.fabManageTransfer.apply {
            setBackgroundColor(
                if (viewModel.selectClients.size != 2)
                    getColor(R.color.colorPrimaryDark)
                else
                    getColor(R.color.colorSecondaryDark)
            )
        }
    }

}