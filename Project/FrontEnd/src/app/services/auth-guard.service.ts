import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { HomeGuard } from './home-gaurd';

@Injectable()
export class AuthGuard implements CanActivate {

  private authorized: boolean;
  
  constructor(private route: Router, private home: HomeGuard) { 
    this.authorized = false;
  }

  setAuthorized(setAuth: boolean) {
     this.authorized = setAuth;
  }

  getAuthorized() {
    return this.authorized;
  }

  canActivate() {
    if (!this.authorized) {
      this.route.navigate(['/login']);
    }
    return this.authorized;
  }
}