import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { BroadcastComponent } from './broadcast/broadcast.component';
import { PrivatemessageComponent } from './privatemessage/privatemessage.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { AuthGuardService } from './services/auth-guard.service';

const routes: Routes = [
  {path:'login', component: LoginComponent, pathMatch: 'full'},
  { path: 'broadcast', component: BroadcastComponent, pathMatch: 'full', canActivate: [AuthGuardService]},
  { path: 'message', component: PrivatemessageComponent, pathMatch: 'full', canActivate: [AuthGuardService]},
  {path:'**', component: PageNotFoundComponent, pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { 

}
