/// Handcrafted fuzzer (example)

#include "time.hpp"

#include <cstdint>
#include <iterator> // for std::size

// Constructor section

struct ConstructorData {
    size_t arg_size;
    Time (*fn)(const uint8_t *);
};


Time constructor1(const uint8_t *data) {
    size_t size = 0;

    // args

    // call
    return Time();
}

Time constructor2(const uint8_t *data) {
    size_t size = 0;

    // args
    const uint *arg1 = reinterpret_cast<const uint*>(data + size);
    size += sizeof(uint);

    // call
    return Time(*arg1);
}

const ConstructorData constr_list[] = {
    {
        .arg_size = 0,
        .fn = constructor1,
    },
    {
        .arg_size = sizeof(uint),
        .fn = constructor2,
    }
};
constexpr size_t constr_size = std::size(constr_list);

// Method section

struct MethodData {
    size_t arg_size;
    void (*fn)(Time *, const uint8_t *);
};

void method_set(Time *obj, const uint8_t *data) {
    size_t size = 0;

    // args
    const uint *arg1 = reinterpret_cast<const uint*>(data + size);
    size += sizeof(uint);
    
    // call
    obj->set(*arg1);
}

void method_zero(Time *obj, const uint8_t *data) {
    size_t size = 0;

    // args
    
    // call
    obj->zero();
}

void method_get(Time *obj, const uint8_t *data) {
    size_t size = 0;

    // args
    
    // call
    obj->get();
}

void method_secs(Time *obj, const uint8_t *data) {
    size_t size = 0;

    // args
    
    // call
    obj->secs();
}

void method_is_zero(Time *obj, const uint8_t *data) {
    size_t size = 0;

    // args
    
    // call
    obj->is_zero();
}

const MethodData method_list[] = {
    {
        .arg_size = sizeof(uint),
        .fn = method_set,
    },
    {
        .arg_size = 0,
        .fn = method_zero,
    },
    {
        .arg_size = 0,
        .fn = method_get,
    },
    {
        .arg_size = 0,
        .fn = method_secs,
    },
    {
        .arg_size = 0,
        .fn = method_is_zero,
    },
};
constexpr size_t method_size = std::size(method_list);


extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    //  supported up to 255 constructors and methods

    // empty string
    if (size == 0)
        return 0;

    // get constr id
    size_t args = 0;
    auto c = constr_list[data[args] % constr_size];
    args += 1;

    // check if we have enough space for arguments
    if (args + c.arg_size > size)
        return 0;
    
    // call constructor
    auto obj = c.fn(data + args);
    args += c.arg_size;

    // check if we have enough space for method id
    if (args >= size)
        return 0;

    // get method
    auto m = method_list[data[args] % method_size];
    args += 1;

    while (args + m.arg_size <= size) {
        // call method
        m.fn(&obj, data + args);
        args += m.arg_size;

        // check if we have space for another method
        if (args >= size)
            return 0;

        // get new method
        m = method_list[data[args] % method_size];
        args += 1;
    }
    
    return 0;
}