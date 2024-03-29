import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { BroadcastComponent } from './broadcast/broadcast.component';
import { PrivatemessageComponent } from './privatemessage/privatemessage.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { AuthGuard } from './services/auth-guard.service';
import { GroupComponent } from './group/group.component';
import { UsersComponent } from './users/users.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent, pathMatch: 'full'},
  { path: 'broadcast', component: BroadcastComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'reports', component: UsersComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'message', component: PrivatemessageComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'group', component: GroupComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: '', redirectTo: 'login', pathMatch: 'full'},
  {path:'**', component: PageNotFoundComponent, pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { 

}
