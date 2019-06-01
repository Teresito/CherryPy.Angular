import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';

@Injectable()
export class HomeGuard implements CanActivate {

  private loggedIn: boolean;
  
  constructor(private route: Router) { 
    this.loggedIn = true;
  }

  setLoggedIn(loggedIn: boolean){
    this.loggedIn = loggedIn
  }

  canActivate() {
    return this.loggedIn;
  }
}