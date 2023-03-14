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

        cy.contains('Host Login').click()
        cy.contains('Sign Up').click()
        cy.get('[placeholder="Email"]').type('host4@163.com')
        cy.get('[placeholder="Password"]').type('Ab123456!')
        cy.get('[placeholder="Confirm Password"]').type('Ab123456!')
        cy.get('.Register').click()
        cy.contains('Reset Password').click()
        cy.get('[placeholder="Old Password"]').type('Ab123456!')
        cy.get('[placeholder="New Password"]').type('Aa123456!')
        cy.get('[placeholder="Confirm Password"]').type('Aa123456!')
        cy.get('.submit1').click()
        cy.contains('Logout').click()
        cy.contains('Host Login').click()
        cy.get('[placeholder="Email"]').type('host4@163.com')
        cy.get('[placeholder="Password"]').type('Aa123456!')
        cy.get('.Login').click()




      // cy.get('placeholder="Email"')
    })
  })