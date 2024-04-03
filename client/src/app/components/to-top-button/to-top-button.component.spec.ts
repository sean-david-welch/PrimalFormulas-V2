import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ToTopButtonComponent } from './to-top-button.component';

describe('ToTopButtonComponent', () => {
  let component: ToTopButtonComponent;
  let fixture: ComponentFixture<ToTopButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ToTopButtonComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ToTopButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
