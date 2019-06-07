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

  listener = new Subscription;
  
  showNav: boolean = false;

  private reportTimer: any;
  private usersTimer: any;

  constructor(private state: componentState, private API: apiServices, private router: Router ){

  }

  ngOnInit(){
    this.showNav = this.state.getAuth();
    this.listener = this.state.clientState.subscribe(
      ()=>{
        this.showNav = this.state.getAuth();
        console.log(this.state.getAuth())
      });
    }
    
  ngOnDestroy(){
    this.listener.unsubscribe();  

  }

}