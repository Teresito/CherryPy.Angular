import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { HomeGuard } from './home-gaurd';
import { componentState } from './componentService';

@Injectable()
export class AuthGuard implements CanActivate {
 
  constructor(private route: Router, private state: componentState) {}

  canActivate() {
    if (!this.state.loggedIn) {
      this.route.navigate(['/login']);
    }
    return this.state.loggedIn;
  }
}