import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { PrivatemessageComponent } from './privatemessage/privatemessage.component';
import { NavigationbarComponent } from './navigationbar/navigationbar.component';
import { BroadcastComponent } from './broadcast/broadcast.component';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { AuthGuard } from './services/auth-guard.service';
import { apiServices } from './services/apiServices';
import { componentState } from './services/componentService';
import { GroupComponent } from './group/group.component';
import { AccountComponent } from './account/account.component';
import { PrivatedataComponent } from './privatedata/privatedata.component';
import { UserListComponent } from './user-list/user-list.component';
import { UsersComponent } from './users/users.component';
import { MarkdownModule, MarkedOptions } from 'ngx-markdown';

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
    PrivatedataComponent,
    UserListComponent,
    UsersComponent,
    
  ],
  imports: [
    BrowserModule,
    FormsModule,
    MarkdownModule.forRoot({
      loader: HttpClient, // optional, only if you use [src] attribute
      markedOptions: {
        provide: MarkedOptions,
        useValue: {
          gfm: true,
          tables: true,
          breaks: false,
          pedantic: false,
          sanitize: true,
          smartLists: true,
          smartypants: false,
        },
      },
    }),
    ReactiveFormsModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [apiServices, componentState, AuthGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
