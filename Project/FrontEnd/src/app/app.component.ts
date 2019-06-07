import { Component, OnInit, OnDestroy, AfterViewInit, HostListener } from '@angular/core';
import { componentState } from './services/componentService';
import { Subscription } from 'rxjs';
import { apiServices } from './services/apiServices';
import { NavigationStart, Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy, AfterViewInit {
  @HostListener('window:beforeunload')

  listener = new Subscription;
  
  showNav: boolean = false;

  private reportTimer: any;
  private usersTimer: any;
  private checkTimer: any;

  constructor(private state: componentState, private API: apiServices, private router: Router ){

  }

  ngOnInit(){

    this.showNav = this.state.getAuth();
    this.listener = this.state.clientState.subscribe(
      ()=>{
        this.showNav = this.state.getAuth();
      });
    this.state.session.subscribe(
      () => { 
        if(Boolean(sessionStorage.getItem('inSession'))){
          this.reportTimer = setInterval(()=>{
            this.API.reportUser();
          },10000);

          this.usersTimer = setInterval(()=>{
            this.state.usersList = this.API.listUserAPI();
          },30000);

          this.checkTimer = setInterval(()=>{
            console.log('CAllED')
            this.API.checkClients().then();
          },60000)
        }
        else{
          clearInterval(this.reportTimer);
          clearInterval(this.checkTimer);
          clearInterval(this.usersTimer);
        }
      }
    )
  }

  logout() {
    this.API.logoutAPI();
    this.state.clearClient();
  }
  
  ngAfterViewInit(){

    
  }

  ngOnDestroy(){
    this.listener.unsubscribe();  

  }

}