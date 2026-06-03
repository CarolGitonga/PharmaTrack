import { HttpInterceptorFn, HttpRequest, HttpHandlerFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, switchMap, throwError } from 'rxjs';
import { AuthService } from './auth.service';
import { environment } from '../../../environments/environment';

let refreshing = false;

function withToken(req: HttpRequest<unknown>, token: string): HttpRequest<unknown> {
  return req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
}

export const jwtInterceptor: HttpInterceptorFn = (req: HttpRequest<unknown>, next: HttpHandlerFn) => {
  const auth = inject(AuthService);
  const http = inject(HttpClient);
  const token = auth.getAccessToken();

  const authedReq = token ? withToken(req, token) : req;

  return next(authedReq).pipe(
    catchError((err: HttpErrorResponse) => {
      const refreshToken = localStorage.getItem('refresh_token');

      if (err.status !== 401 || !refreshToken || refreshing) {
        if (err.status === 401) auth.logout();
        return throwError(() => err);
      }

      refreshing = true;
      return http.post<{ access: string }>(`${environment.apiUrl}/auth/token/refresh/`, { refresh: refreshToken }).pipe(
        switchMap(({ access }) => {
          refreshing = false;
          localStorage.setItem('access_token', access);
          return next(withToken(req, access));
        }),
        catchError((refreshErr) => {
          refreshing = false;
          auth.logout();
          return throwError(() => refreshErr);
        }),
      );
    }),
  );
};
