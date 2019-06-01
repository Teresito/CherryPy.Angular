import { Component, OnInit, OnDestroy } from '@angular/core';
import { componentState } from './services/componentService';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy{

  valid: boolean = false;
  subscription: Subscription;
  constructor(private state: componentState){}

  ngOnInit(){
    this.subscription = this.state.loggedChanged.subscribe(()=>{
      this.valid = this.state.getLoggedIn();
    });
  }

  ngOnDestroy(){
    //this.subscription.unsubscribe;
  }

}

