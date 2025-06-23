import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface Message {
  sender: 'user' | 'assistant';
  text: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.css'
})
export class Chat {
  messages: Message[] = [];
  userInput = '';
  loading = false;
  error = '';

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}

  sendMessage() {
    if (!this.userInput.trim()) return;
    const userMsg: Message = { sender: 'user', text: this.userInput };
    this.messages.push(userMsg);
    this.loading = true;
    this.error = '';
    const question = this.userInput;
    this.userInput = '';
    this.http.get<{ answer: string }>('/query/', { params: { q: question } }).subscribe({
      next: (res) => {
        this.messages.push({ sender: 'assistant' as const, text: res.answer });
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: err => {
        this.error = err.error?.detail || 'Error getting response';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }
}
