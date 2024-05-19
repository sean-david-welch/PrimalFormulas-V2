package models

import (
	"github.com/google/uuid"
	"time"
)

type User struct {
	ID       string `json:"id"`
	Username string `json:"username"`
	Password string `json:"password"`
	Created  string `json:"created"`
}

func NewUser(username, password string) *User {
	return &User{
		ID:       uuid.New().String(),
		Username: username,
		Password: password,
		Created:  time.Now().UTC().Format(time.RFC3339),
	}
}
