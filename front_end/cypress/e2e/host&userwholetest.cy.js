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
      
      cy.contains('New Activity').click()
      cy.get('[placeholder="Activity Name"]').type('music activity')
      
      cy.get('.MuiSelect-select').click()
      cy.contains('Music').click()
      cy.get('[placeholder="Venue Name"]').type('road')
      cy.get('[placeholder="Venue Address"]').type('road 1st')
      cy.get('[placeholder="Description"]').type('good')
      cy.get('[placeholder="Possible Seats"]').type('10')
      cy.get('[placeholder="Row"]').type('10')
      cy.get('[placeholder="Column"]').type('10')
      cy.get('[placeholder="Ticket Money"]').type('10')
      cy.get('[placeholder="All Tickets"]').type('10')
      cy.get('[placeholder="Paste image link"]').type(' ')
      cy.get('input[placeholder="Start Time"]').type('2018-06-06T08:30')
      cy.get('input[placeholder="End Time"]').type('2019-06-07T08:30')
      cy.contains('Submit').click()

      cy.contains('Your Activities').click()
      cy.contains('Broadcast').click()
      cy.get('input[placeholder="message"]').type('hello')
      cy.get('.boradcast').click()

      // cy.contains('Your Activities').click()

      // cy.get('.productListEdit').filter(':contains("Cancel")').click()

      // cy.get('.MuiButton-label').filter(':contains("Ok")').click()
      // cy.contains('Cancel').click()
      // cy.contains('OK').click()


      cy.contains('New Activity').click()
      cy.get('[placeholder="Activity Name"]').type('magic activity')
      
      cy.get('.MuiSelect-select').click()
      cy.contains('Magical').click()
      cy.get('[placeholder="Venue Name"]').type('road')
      cy.get('[placeholder="Venue Address"]').type('road 1st')
      cy.get('[placeholder="Description"]').type('good')
      cy.get('[placeholder="Possible Seats"]').type('10')
      cy.get('[placeholder="Row"]').type('10')
      cy.get('[placeholder="Column"]').type('10')
      cy.get('[placeholder="Ticket Money"]').type('10')
      cy.get('[placeholder="All Tickets"]').type('10')
      cy.get('[placeholder="Paste image link"]').type(' ')
      cy.get('input[placeholder="Start Time"]').type('2018-06-06T08:30')
      cy.get('input[placeholder="End Time"]').type('2019-06-07T08:30')
      cy.contains('Submit').click()

      cy.contains('Logout').click()


      cy.visit('http://localhost:3000/time_set')
      cy.get('input[name="time"]').type('2017-08-01T08:30:01')
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



    cy.contains('My Detail').click()
    cy.contains('Edit Detail').click()
    cy.get('[placeholder="first name"]').type('Tom')
    cy.get('[placeholder="last name"]').type('Li')
    cy.get('[placeholder="address"]').type('sunshine road 1st')
    cy.get('.update').click()

    cy.contains('Edit Account').click()
    cy.contains('Bpay').click()
    cy.get('[placeholder="Name"]').type('name')
    cy.get('[placeholder="BSB 6 digits"]').type('111111')
    cy.get('[placeholder="Account Number 8 digits"]').type('11111111')
    cy.get('.submit3').click()
    
    cy.contains('Add Balance').click()
    cy.get('button').filter(':contains("+ 50")').click()
    cy.get('button').filter(':contains("Submit")').click()

    cy.contains('Search').click()
    cy.get('.featuredImg').last().click({force: true})
    cy.get('[name = "seat_x"]').type('1')
    cy.get('[name = "seat_y"]').type('1')
    cy.contains('Buy Tickets').click()
    cy.contains('Ok').click()

    cy.contains('Your Activities').click()
    cy.contains('host4@163.com').click()
    cy.contains('Subscribe').click()
    cy.contains('Unsubscribe').click()
    cy.contains('Home').click()

    })
  })