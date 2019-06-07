import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { componentState } from './componentService';

@Injectable()
export class AuthGuard implements CanActivate {
 
  constructor(private route: Router, private state: componentState) {}

  canActivate() {
    if (!this.state.getAuth()){
      this.route.navigate(['/login']);
    }
    return this.state.getAuth();
  }
  
}