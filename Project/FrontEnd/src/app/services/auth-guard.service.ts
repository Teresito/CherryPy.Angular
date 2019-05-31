import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';

@Injectable()
export class AuthGuardService implements CanActivate {

  private authorized: boolean = false;

  constructor(private route: Router) { }

  setAuthorized(setAuth: boolean){
    this.authorized = setAuth;
  }

  canActivate() {
    if (!this.authorized) {
      this.route.navigate(['/login']);
    }
    return this.authorized;
  }
}