#pragma once
#include <string> 
#include <map>
template<typename T, typename U > class State
{
    public:
        State() :
            in_(nullptr),
            out_(nullptr)
        {}
        virtual ~State() {}
        void link( T *in , U *out)
        {
            in_ =in ;
            out_ = out;
        }
        virtual std::string update()=0;
    protected:
        T *in_;
        U *out_;
};

template< typename T, typename U > class StateMachine
{
    public:
    StateMachine()
    {

    }
    ~StateMachine()
    {

    }
    void add( std::string name , State<T,U> *state)
    {
        state->link( &in_ , &out_  );
        std::pair< std::string , State<T,U>*> i( name ,state);
        stateMap_.insert( i );
    }
    void forceState(std::string name)
    {
        current_ = stateMap_.at( name );
    }
    void update( )
    {

        std::string next;
        next = current_->update();
        current_ = stateMap_.at( next );

    }
    void set( const T &in)
    {
        in_ = in;
    }
    U get()
    {
        return out_;
    }
    protected:
        State<T,U> *current_;
        T in_;
        U out_;
        std::map< std::string , State<T,U>* >stateMap_; 
};
