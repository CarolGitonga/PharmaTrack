import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

export interface ConfirmDialogData {
  title: string;
  message: string;
  confirmText?: string;
  confirmColor?: 'warn' | 'primary';
}

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [CommonModule, MatDialogModule, MatButtonModule, MatIconModule],
  template: `
    <div class="dialog-container">
      <div class="dialog-icon">
        <mat-icon>warning_amber</mat-icon>
      </div>
      <h3 class="dialog-title">{{ data.title }}</h3>
      <p class="dialog-message">{{ data.message }}</p>
      <div class="dialog-actions">
        <button class="cancel-btn" mat-dialog-close>Cancel</button>
        <button class="confirm-btn" [mat-dialog-close]="true">
          {{ data.confirmText || 'Confirm' }}
        </button>
      </div>
    </div>
  `,
  styles: [`
    .dialog-container {
      padding: 28px 24px 20px;
      text-align: center;
      max-width: 360px;
    }
    .dialog-icon {
      width: 52px; height: 52px; border-radius: 50%;
      background: #fef2f2; display: flex; align-items: center;
      justify-content: center; margin: 0 auto 16px;
      mat-icon { color: #ef4444; font-size: 26px; width: 26px; height: 26px; }
    }
    .dialog-title {
      margin: 0 0 8px; font-size: 17px; font-weight: 700; color: #0f172a;
    }
    .dialog-message {
      margin: 0 0 24px; font-size: 14px; color: #64748b; line-height: 1.5;
    }
    .dialog-actions {
      display: flex; gap: 10px; justify-content: center;
    }
    .cancel-btn {
      padding: 0 24px; height: 40px; border-radius: 8px;
      border: 1.5px solid #e2e8f0; background: #fff;
      color: #64748b; font-size: 14px; font-weight: 600;
      font-family: inherit; cursor: pointer;
      &:hover { border-color: #94a3b8; }
    }
    .confirm-btn {
      padding: 0 24px; height: 40px; border-radius: 8px;
      border: none; background: #ef4444; color: #fff;
      font-size: 14px; font-weight: 600;
      font-family: inherit; cursor: pointer;
      &:hover { background: #dc2626; }
    }
  `],
})
export class ConfirmDialogComponent {
  data: ConfirmDialogData = inject(MAT_DIALOG_DATA);
  ref = inject(MatDialogRef<ConfirmDialogComponent>);
}
