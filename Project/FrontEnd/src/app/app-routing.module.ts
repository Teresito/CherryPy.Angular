import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { BroadcastComponent } from './broadcast/broadcast.component';
import { PrivatemessageComponent } from './privatemessage/privatemessage.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const routes: Routes = [
  {path:'', component: LoginComponent, pathMatch: 'full'},
  {path:'broadcast', component: BroadcastComponent, pathMatch: 'full'},
  {path:'message', component: PrivatemessageComponent, pathMatch: 'full'},
  {path:'**', component: PageNotFoundComponent, pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { 

}
