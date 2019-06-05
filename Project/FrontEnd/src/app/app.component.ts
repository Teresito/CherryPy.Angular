import { Component, OnInit, OnDestroy } from '@angular/core';
import { componentState } from './services/componentService';
import { Subscription } from 'rxjs';
import { apiServices } from './services/apiServices';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {

  valid: boolean = false;
  subscription: Subscription;
  constructor(private state: componentState, private API: apiServices, private router: Router ){}

  ngOnInit(){
    this.subscription = this.state.loggedChanged.subscribe(
      ()=>{
        if(this.state.getLoggedIn()){
          this.valid = true;
        }
        else{
          this.valid = false;
          this.router.navigate(['/login']);
        }
      }
    );
  }

  ngOnDestroy(){
    this.subscription.unsubscribe;
  }

}