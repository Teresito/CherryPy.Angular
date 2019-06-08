import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { componentState } from './componentService';

@Injectable()
export class AuthGuard implements CanActivate {
 
  constructor(private route: Router, private state: componentState) {}

  canActivate() {
    let auth = Boolean(sessionStorage.getItem('authenticated'));
    if (!auth){
      this.route.navigate(['/login']);
    }
    return auth;
  }
  
}