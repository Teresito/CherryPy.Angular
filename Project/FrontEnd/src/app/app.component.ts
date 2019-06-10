import { Component, OnInit, OnDestroy, AfterViewInit, HostListener } from '@angular/core';
import { componentState } from './services/componentService';
import { Subscription } from 'rxjs';
import { apiServices } from './services/apiServices';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  @HostListener('window:beforeunload')

  listener = new Subscription;

  showNav: boolean = false;

  private reportTimer: any;
  private usersTimer: any;

  constructor(private state: componentState, private API: apiServices) {

  }
  // Initialize the component with these parameters and function calls
  ngOnInit() {

    this.showNav = this.state.getAuth();
    if (sessionStorage.getItem('status') == '' && Boolean(sessionStorage.getItem('authenticated'))) {
      sessionStorage.setItem('status', 'online')
    }
    this.listener = this.state.clientState.subscribe(
      () => {
        this.showNav = this.state.getAuth();
      });

    this.StartnEndTimers();


    this.state.session.subscribe(() => {
      this.StartnEndTimers();
    });



  }
  // Start reporting the user and starts updating the list
  StartnEndTimers() {
    if (Boolean(sessionStorage.getItem('inSession'))) {
      this.reportTimer = setInterval(() => {
        this.API.reportUser();
      }, 10000);

      this.usersTimer = setInterval(() => {
        this.state.usersList = this.API.listUserAPI();
      }, 30000);

    }
    else {
      clearInterval(this.reportTimer);
      clearInterval(this.usersTimer);
    }
  }
  // User has logged out
  logout() {
    this.API.logoutAPI();
    this.state.clearClient();
  }

  ngOnDestroy() {
    this.listener.unsubscribe();

  }

}