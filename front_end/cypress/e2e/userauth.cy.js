describe('empty spec', () => {
    it('passes', () => {
      // cy.visit('https://example.cypress.io')
      cy.visit('http://localhost:3000/time_set')
      cy.get('input[name="time"]').type('2017-06-01T08:30:01')
      cy.contains(' Set Time ').click()

      cy.contains('Clear Data').click()

      cy.visit('http://localhost:3000/time_set')
      cy.get('input[name="time"]').type('2017-06-01T08:30:01')
      cy.contains(' Set Time ').click()

      cy.contains('User Login').click()
      cy.contains('Sign Up').click()
      cy.get('[placeholder="Email"]').type('user4@163.com')
      cy.get('[placeholder="Password"]').type('Ab123456!')
      cy.get('[placeholder="First Name"]').type('Sam')
      cy.get('[placeholder="Last Name"]').type('Smith')
      cy.get('[placeholder="Address"]').type('1 Lorn St')
      cy.contains('WeChat').click()
      cy.get('[placeholder="Account 3-40 characters"]').type('661133')
      cy.get('.userSign').click()

      cy.contains('Reset Password').click()
      cy.get('[placeholder="Old Password"]').type('Ab123456!')
      cy.get('[placeholder="New Password"]').type('Aa123456!')
      cy.get('[placeholder="Confirm Password"]').type('Aa123456!')
      cy.get('.reset123').click()
      cy.wait(100)
      cy.contains('Logout').click()
      cy.contains('User Login').click()
      cy.get('[placeholder="Email"]').type('user4@163.com')
      cy.get('[placeholder="Password"]').type('Aa123456!')
      cy.get('.userLogin').click()
      
    })
  })