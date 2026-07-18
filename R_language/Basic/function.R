"""GCD is used to find greatest common divisor of two integer
  gcd(3,9) return 3"""
gcd <- function(a,b){
  if(b==0){
    return(a)
  }else{
    return(gcd(b,a%%b))    
  }
}
"""LCM is used to find lowest common multiple of two integer
  lcm(3,5) return 15"""
lcm <- function(a,b){
  return ((a*b)/gcd(a,b))
}
Fibonacci <- function(n){
  if (n<0){
    print("Incorrect input")
  }else if (n==0){
    return(0)
  }else if (n==1){
    return(1)
  }else{
    return(Fibonacci(n-1)+Fibonacci(n-2))
  }
    
}
fact <-function(n){
  if(n==0){
    return(1)
    
  }else if(n==1){
    return(1)
  }else{
    return(n * fact(n - 1))
  }
}
nCr<-function(n,r){
    '''
    Returns the Binomial Coefficient.
    Parameters:
        n (int): 0 <= n.
    Returns:
        (int) : return nCr(n, r) values and 1 for -ve values.
    '''
    return(fact(n)//(fact(n-r)*fact(r)))
 }
nPr<-function(n,r){
    '''
    Returns the Permutations.
    Parameters:
        n (int): 0 <= n.
    Returns:
        (int) : return nPr(n, r) values.
    '''
    return  fact(n)//fact(n-r)
