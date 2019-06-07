import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { apiServices } from '../services/apiServices';
import { AuthGuard } from '../services/auth-guard.service';
import { componentState } from '../services/componentService';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-navigationbar',
  templateUrl: './navigationbar.component.html',
  styleUrls: ['./navigationbar.component.css']
})
export class NavigationbarComponent implements OnInit {

  zIndex: boolean = true;
  listener = new Subscription;
  constructor(private route: Router, private api: apiServices, private state: componentState) { }

  ngOnInit() {

  }

  logout(){  

  }


}
