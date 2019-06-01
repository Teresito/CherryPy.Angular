import { Subject } from 'rxjs';

export class componentState {
    eKeyNotify = true;
    loggedChanged = new Subject<any>();

    setLoggedIn(bool: boolean){
        sessionStorage.setItem('loggedIn', String(bool));
    }

    getLoggedIn(){
        return Boolean(sessionStorage.getItem('loggedIn'));
    }

    deleteSession(){
        sessionStorage.clear();
    }


}