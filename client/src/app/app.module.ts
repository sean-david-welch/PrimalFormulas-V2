import { NgModule } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  imports: [FontAwesomeModule],
  bootstrap: [HttpClientModule],
})
export class AppModule {}
