package org.cnsl.ftms.di

import androidx.recyclerview.widget.RecyclerView
import org.cnsl.ftms.repository.local.entities.Client
import org.cnsl.ftms.viewmodel.EditClientViewModel
import org.cnsl.ftms.viewmodel.ManageViewModel
import org.cnsl.ftms.viewmodel.RegisterClientViewModel
import org.cnsl.ftms.viewmodel.TransferViewModel
import org.koin.androidx.viewmodel.dsl.viewModel
import org.koin.dsl.module

val manageModule = module {
    viewModel { (view: RecyclerView) -> ManageViewModel(get(), view) }
}

val registerModule = module {
    viewModel { RegisterClientViewModel(get()) }
}

val editModule = module {
    viewModel { (client: Client) -> EditClientViewModel(get(), client) }
}

val transferModule = module {
    viewModel { (client_a: Client, client_b: Client) -> TransferViewModel(get(), client_a, client_b) }
}

val allModules = manageModule + registerModule + editModule + transferModule