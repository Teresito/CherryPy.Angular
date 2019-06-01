import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { PrivatemessageComponent } from './privatemessage/privatemessage.component';
import { NavigationbarComponent } from './navigationbar/navigationbar.component';
import { BroadcastComponent } from './broadcast/broadcast.component';
import { HttpClientModule } from '@angular/common/http';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { AuthGuard } from './services/auth-guard.service';
import { apiServices } from './services/apiServices';
import { componentState } from './services/componentService';
import { GroupComponent } from './group/group.component';
import { AccountComponent } from './account/account.component';
import { HomeGuard } from './services/home-gaurd';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    PrivatemessageComponent,
    NavigationbarComponent,
    BroadcastComponent,
    PageNotFoundComponent,
    GroupComponent,
    AccountComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [apiServices, componentState, AuthGuard,HomeGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
