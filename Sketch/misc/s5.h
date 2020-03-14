#ifndef S5_H
#define S5_H

#include <cstring>

#include "vops.h"

namespace ANONYMOUS{
}
namespace list{
template<typename T>
class List; 
template<typename T>
class Cons; 
template<typename T>
class Nil; 
}
namespace ANONYMOUS{
extern void main__Wrapper();
extern void main__WrapperNospec();
extern void _main();
extern void mypos(list::List<int > * a, list::List<int > *& _out);
extern void equals_List_s0(list::List<int > * left_s1, list::List<int > * right_s2, int bnd_s3, bool& _out);
extern void empty_list(list::List<int > *& _out);
extern void ifelist(list::List<int > * a, list::List<int > *& _out);
}
namespace list{
template<typename T>
class List; 
template<typename T>
class Cons; 
template<typename T>
class Nil; 
template<typename T>
class List{
  public:
  typedef enum {CONS_type, NIL_type} _kind;
  _kind type;
  ~List(){
  }
  void operator delete(void* p){ free(p); }
};
template<typename T>
class Cons : public List<T>{
  public:
  T  val;
  List<T > *  next;
  Cons(){}
  static Cons* create(  T  val_,   List<T > *  next_);
  ~Cons(){
  }
  void operator delete(void* p){ free(p); }
};
template<typename T>
class Nil : public List<T>{
  public:
  static Nil* create();
  ~Nil(){
  }
  void operator delete(void* p){ free(p); }
};
template<typename T>
extern void empty(List<T > *& _out);
template<typename T>
extern void add(List<T > * lst, T val, List<T > *& _out);
template<typename T>
extern void head(List<T > * l, T& _out);
}

#endif
