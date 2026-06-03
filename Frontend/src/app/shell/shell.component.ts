import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { AuthService } from '../core/auth/auth.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterModule, CommonModule, MatIconModule, MatButtonModule, MatTooltipModule],
  templateUrl: './shell.component.html',
  styleUrl: './shell.component.scss',
})
export class ShellComponent {
  private auth = inject(AuthService);
  user = this.auth.getUser();

  get initials(): string {
    const u = this.user;
    if (!u) return '?';
    const first = u.first_name?.[0] || '';
    const last = u.last_name?.[0] || '';
    if (first && last) return (first + last).toUpperCase();
    if (first) return first.toUpperCase();
    return (u.username?.[0] || '?').toUpperCase();
  }

  logout(): void {
    this.auth.logout();
  }
}
