import { Component, OnInit, OnDestroy } from '@angular/core';
import { componentState } from './services/componentService';
import { Subscription } from 'rxjs';
import { apiServices } from './services/apiServices';
import { NavigationStart, Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {

  valid: boolean = false;
  subscription: Subscription;
  constructor(private state: componentState, private API: apiServices, private router: Router ){
    this.subscription = router.events.subscribe((event) => {
      if (event instanceof NavigationStart) {
        this.state.loggedChanged.next();
      }
    });
  }

  ngOnInit(){
    this.subscription = this.state.loggedChanged.subscribe(
      ()=>{
        this.valid = this.state.getLoggedIn();
      }
    );

  }

  ngOnDestroy(){
    this.subscription.unsubscribe;
  }

}