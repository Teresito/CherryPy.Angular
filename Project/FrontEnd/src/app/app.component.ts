import { Component, OnInit } from '@angular/core';
import { componentState } from './services/componentService';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{

  valid: boolean = false;

  constructor(private state: componentState){}

  ngOnInit(){
    this.state.loggedChanged.subscribe(()=>{
      this.valid = this.state.loggedIn;
    });
  }

}

