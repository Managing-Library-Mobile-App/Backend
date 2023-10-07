Tests were split into 5 categories:
- Functional - ensures the API performs exactly as it is supposed to. 
This test analyzes specific functions within the codebase to guarantee the API functions 
within its expected parameters and can handle errors when the results are outside the designated parameters.
Consists of: 
    black box testing
    white box testing
    smoke testing - verification before changing the code
    sanity testing - verification if the code still works after changes
    user acceptance testing
    integration testing
    unit testing

- Fuzz and load - forcibly inputs huge amounts of random data -- also called noise or fuzz -- 
into the system, attempting to create negative behavior, such as a forced crash or overflow. 
Seeing how many calls an API can handle. This test is often performed 
after a specific unit or codebase is completed to determine whether the theoretical solution 
can also work as a practical solution when acting under a given load.

- Security - attempts to validate the encryption methods the API uses 
as well as the access control design. It includes the validation of authorization 
checks for resource access and user rights management.

Individual tests are split into three parts:
- GIVEN - Initial state and values
- WHEN - Tested behavior
- THEN - Expected results