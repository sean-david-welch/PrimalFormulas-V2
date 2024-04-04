import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AboutFormComponent } from './about-form.component';

describe('AboutFormComponent', () => {
  let component: AboutFormComponent;
  let fixture: ComponentFixture<AboutFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AboutFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AboutFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
