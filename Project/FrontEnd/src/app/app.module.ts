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
import { apiServices } from './services/apiServices';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    PrivatemessageComponent,
    NavigationbarComponent,
    BroadcastComponent,
    PageNotFoundComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [apiServices],
  bootstrap: [AppComponent]
})
export class AppModule { }
