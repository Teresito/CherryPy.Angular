import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { apiServices } from '../services/apiServices';
import { AuthGuard } from '../services/auth-guard.service';
import { componentState } from '../services/componentService';
import { Subscription } from 'rxjs';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-navigationbar',
  templateUrl: './navigationbar.component.html',
  styleUrls: ['./navigationbar.component.css']
})
export class NavigationbarComponent implements OnInit {

  zIndex: boolean = true;
  listener = new Subscription;
  status = new FormControl('');
  search = new FormControl('');
  statusList = ['Online', 'Away', 'Busy', 'Offline']
  user: string;
  constructor(private route: Router, private API: apiServices, private state: componentState) { }

  ngOnInit() {
    this.zIndex = !Boolean(sessionStorage.getItem('inSession'))
    this.user = sessionStorage.getItem('username')
    this.state.session.subscribe(() => {
      if (Boolean(sessionStorage.getItem('inSession'))) {
        this.zIndex = false;
        this.user = sessionStorage.getItem('username')
      }
    })
  }

  onKeydown(event) {
    this.searchUser();
  }

  searchUser(){
    this.state.searchTrigger.next(this.search.value);
  }

  changedStatus() {
    sessionStorage.setItem('status', this.status.value.toLowerCase())
  }

  logout() {
    this.state.clearClient();
    this.API.logoutAPI();
  }


}
