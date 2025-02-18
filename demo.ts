/*
 * @Author: Diana Tang
 * @Date: 2025-02-18 10:05:39
 * @LastEditors: Diana Tang
 * @Description: some description
 * @FilePath: /add-srt-compress-video/demo.ts
 */

type First<T extends any[]> = T extends [] ? never : T[0];

// Test cases for First<T>
type arr1 = ['a', 'b', 'c'];
type arr2 = [3, 2, 1];
type emptyArr = [];

type head1 = First<arr1>; // 'a'
type head2 = First<arr2>; // 3
type head3 = First<emptyArr>; // never

// Last<T> implementation
type Last<T extends any[]> = T extends [...any[], infer L] ? L : never;

// Test cases for Last<T>
type tail1 = Last<arr1>; // 'c'
type tail2 = Last<arr2>; // 1
type tail3 = Last<emptyArr>; // never

// Additional test cases
type singletonArr = [42];
type head4 = First<singletonArr>; // 42
type tail4 = Last<singletonArr>; // 42
type First<T extends any[]>=T extends []?never:T[0];
type First<T extends any[]>=T['length'] extends 0?never:T[0];
type First<T extends any[]>=T extends [infer F,...any[]]?F :never;
type Last<T extends any[]>=T extends[...any[],infer Last]?Last:never
type Last<T extends any[]>=T['length'] extends 0?never:[never,...T][T['length']]

