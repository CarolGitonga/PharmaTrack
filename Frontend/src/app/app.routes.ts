import { Routes } from '@angular/router';
import { authGuard } from './core/auth/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./features/login/login.component').then(m => m.LoginComponent),
  },
  {
    path: '',
    canActivate: [authGuard],
    loadComponent: () => import('./shell/shell.component').then(m => m.ShellComponent),
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent),
      },
      {
        path: 'medicines',
        loadComponent: () => import('./features/medicines/medicine-list/medicine-list.component').then(m => m.MedicineListComponent),
      },
      {
        path: 'medicines/add',
        loadComponent: () => import('./features/medicines/medicine-form/medicine-form.component').then(m => m.MedicineFormComponent),
      },
      {
        path: 'medicines/edit/:id',
        loadComponent: () => import('./features/medicines/medicine-form/medicine-form.component').then(m => m.MedicineFormComponent),
      },
      {
        path: 'alerts',
        loadComponent: () => import('./features/alerts/alert-settings/alert-settings.component').then(m => m.AlertSettingsComponent),
      },
    ],
  },
  { path: '**', redirectTo: 'dashboard' },
];
