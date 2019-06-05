import { Component, OnInit } from '@angular/core';
import { componentState } from '../services/componentService';
import { apiServices } from '../services/apiServices';

@Component({
  selector: 'app-privatemessage',
  templateUrl: './privatemessage.component.html',
  styleUrls: ['./privatemessage.component.css']
})
export class PrivatemessageComponent implements OnInit {

  convoHistory: boolean = true;
  
  constructor(private state: componentState, private API: apiServices) { }
  
  ngOnInit() {
  
  }


}
