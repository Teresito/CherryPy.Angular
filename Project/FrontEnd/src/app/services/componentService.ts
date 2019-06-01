import { Subject } from 'rxjs';

export class componentState {
    eKeyNotify = true;
    notifyChanged = new Subject<any>();
    loggedChanged = new Subject<any>();

    setLoggedIn(bool: boolean){
        console.log(bool);
        sessionStorage.setItem('loggedIn', String(bool));
    }

    getLoggedIn(){
        return Boolean(sessionStorage.getItem('loggedIn'));
    }

    deleteSession(){
        sessionStorage.clear();
    }


}